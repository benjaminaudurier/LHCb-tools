# =============================================================================
#  @class AnnaFacade
#  @author Benjamin AUDURIER benjamin.audurier@ca.infn.it
#  @date   2017-11-30

# From the framework
from .AnnaConfig import AnnaConfig
from .AnnaFitter import AnnaFitter
# Tuple bank
import TupleFilterBank as TupleFilterBank
from TupleFilterBank import *
# ROOT and Ostap
import ROOT
import Ostap.ZipShelve as DBASE
from Ostap.PyRoUts import *
# Python
import sys
import logging
from logging import debug, error, info, warning
logging.basicConfig(
    # filename='Anna.log',
    format='%(filename)s -- %(funcName)s -- %(levelname)s: \t\t %(message)s',
    level=logging.DEBUG,
    filemode='w+')


# ______________________________________
class AnnaFacade:
    """
    The framework is meant to work inside the LHCb framework
    as it relies on OSTAP for the fits and the saving data.
    So, prior to import this module, the user must be sure to be
    in an Ostap session (lb-run Bender/latest ostap).

    This class takes 3 arguments :
        - data : A first data object.
                Type could be TNtuple, Ostap.ZipShelve, TFile ... depending
                on the method called. See methods for more details.

        - data2 : A second data object, not medatory, but usefull
                    in MC studies for instance (at the moment not implementeds).

        - configfile : read by AnnaConfig to configure
                        our object (See AnnaConfig for details)

    As a facade, each functions call a dedicade class inside the framework who
    actually do the job (exp: fit, print(diagrams ... ).
    See the classes and functions documentations for more details.

    Finally, all produced results are stored in a Ostap.ZipShelve object
    in the same directory where AnnaFacade is used by default. One can
    change the path if need using the config file (see AnnaConfig)
    """

    # ______________________________________
    def __init__(self, data=None, data2=None, configfile=""):
        """ cstr """

        print(" ========== Init AnnaFacade ========== ")

        self.data = data
        self.data2 = data2
        self.configfile = AnnaConfig()

        # Set configfile
        info(" Try to read config file ...")
        if self.configfile.ReadFromFile(configfile) is True:
            info(" config file set !")

        else:
            error("Cannot set config file")

        print(" ========================================= \n\n")

    # ______________________________________
    def __str__(self):
        return "I am your father"

    # ______________________________________
    def CreateFilteredTuple(self, tuple_filter_name='AnnaTupleFilterJpsiPbPb'):
        """
        Fill and save a filtered tuple from self.data after applying cuts
        on leafs.
        """

        print(" ================================================================ ")
        print("     CreateFilteredTuple with Tuple {} ".format(tuple_filter_name))
        print(" ================================================================ \n\n")

        # Check data type
        if self.data is not None:
            if isinstance(self.data, ROOT.TChain) is False:
                error('Need a ROOT.TChain instead of {} !'.format(type(self.data)))
                return
        else:
            error('Need something to run on !')
            return

        for mother_leaf in self.configfile.map['MotherLeaf']:
            if mother_leaf == "#":
                continue
            for daughters_leaf in self.configfile.map['DaughterLeafs']:

                # get the module
                try:
                    module = getattr(TupleFilterBank, tuple_filter_name)
                except AttributeError:
                    error('Cannot find {} module'.format(tuple_filter_name))

                # Instance the object
                try:
                    TupleFilter = getattr(module, tuple_filter_name)(mother_leaf, daughters_leaf)
                except AttributeError:
                    error('Cannot find {} instance'.format(tuple_filter_name))

                # Get the tuple
                ntuple = TupleFilter.GetTuple(self.data)

                if ntuple is not None:
                    self.SaveResult(
                        ntuple,
                        'Tuple/{}'.format(mother_leaf))
                else:
                    error("CreateFilteredTuple: Cannot get Tuple")
                    continue

    # ______________________________________
    def DrawMinv(self, particle_name="JPsi"):
        return

    # ______________________________________
    def DrawFitResults(self, particle_name="JPsi", spectra_name="", filter_name
                    = '', subresults=None):
        """Draw all fit results

        Draw all results/subresults (i.e fit functions) spectras on a single canvas
        for every combination of Centrality/Cut/Leaf cut from the config.

        Arguments:
            particle_name {str} -- (default: {"JPsi"})
            spectra_name {str} -- The name of the spectra
            subresults {list} -- a specific list of subresults if needed

        """

        print(" ================================================================ ")
        print(
            "       DrawFitResults for particle {} and spectra {}"
            .format(particle_name, spectra_name))
        print(" ================================================================ ")

        debug(
            "FitParticle: AnnaConfig map : \n {}"
            .format(self.configfile.map))

        file = self.GetResultFile()
        if file is None:
            return

        # Check data type
        if self.data is not None:
            if isinstance(self.data, DBASE.ZipShelf) is False:
                error('Need a DBASE instead of {} !'.format(type(self.data)))
                return

        for centrality in self.configfile.map['Centrality']:
            for cut in self.configfile.map['CutCombination']:
                for leaf in self.configfile.map['MotherLeaf']:

                    print("---------------------")
                    print("Looking for spectras ...")

                    spectrapath = "{}/FitParticle/{}/{}/{}".format(
                        filter_name,
                        centrality,
                        cut,
                        leaf)

                    spectra = file.get(
                        '{}/{}'
                        .format(spectrapath, spectra_name))

                    if spectra is None:
                        warning(
                            'Cannot find spectra in {}/{}, continue ...'
                            .format(spectrapath, spectra_name))
                        continue

                    spectra.DrawResults(particle_name, subresults)

        file.close()

    # ______________________________________
    def DrawNofWhat(self, particle_name="JPsi"):
        return

    # ______________________________________
    def FitParticle(self, particle_name="JPsi", binning=[], option=""):
        """Main Fit method

        Run over all combination of Centrality/Cut/Leaf from the config.
        The fit process is passed to AnnaFitter class that return an
        AnnaSpectra to be stored in the result TFile.

        Keyword Arguments:
            particle_name {str} -- To set the particle mass
                in AnnaFitter (default: {"JPsi"})
            binning {list} -- Binning conditions for the fit. (default: {[]})
                Should be a list as [str(leaf_name), x.x, x.x, x.x ...]
                example :
                    ["JPSI_PT", 0., 4000., 8000.])
            option {str} -- possible options (for futur dvlp) (default: {""})
        """

        print(" ================================================================ ")
        print("         FitParticle {} for binning {}".format(particle_name, binning))
        print(" ================================================================ ")

        debug(
            "FitParticle: AnnaConfig map : \n {}"
            .format(self.configfile.map))

        # Check data type
        if self.data is not None:
            if isinstance(self.data, ROOT.TNtuple) is False:
                error('Need a ROOT.TNtuple instead of {} !'.format(type(self.data)))
                return
        else:
            error('Need something to run on !')
            return

        for centrality in self.configfile.map['Centrality']:
            for cut in self.configfile.map['CutCombination']:
                for leaf in self.configfile.map['MotherLeaf']:
                    spectrapath = "{}/FitParticle/{}/{}/{}".format(
                        self.data.GetName(),
                        centrality,
                        cut,
                        leaf)
                    fitter = AnnaFitter(particle_name, binning)
                    spectra = fitter.Fit(
                        self.data,
                        leaf,
                        centrality,
                        cut,
                        self.configfile.map['FitType'],
                        option)
                    if spectra is None:
                        error('Cannot get spectra')
                        continue
                    self.SaveResult(spectra, spectrapath)

                    if self.data2 is not None:
                        if isinstance(self.data, ROOT.NTuple):
                            error('Need a ROOT.TNtuple for second data object!')
                            return
                        spectrapath = "{}/FitParticle/{}/{}/{}".format(
                            self.data2.GetName(),
                            centrality,
                            cut,
                            leaf
                        )
                        fitter = AnnaFitter(particle_name, binning)
                        spectra = fitter.Fit(
                            self.data2,
                            leaf,
                            centrality,
                            cut,
                            self.configfile.map['FitType'],
                            option
                        )
                        if spectra is None:
                            error('Cannot get spectra')
                            continue
                        self.SaveResult(spectra, spectrapath)

    # ______________________________________
    def GetResultFile(self):
        """
        Return the result file, creates one if necessary
        """

        file_path = self.configfile.map['ResultFilePath']

        # Check if several entrie
        if file_path is not None:
            if len(file_path) > 1:
                warning(
                    'Many path for the result file are setted ({}), I will take the first one'
                    .format(file_path))
                file_path = file_path[0]

            # If the storing file is elsewhere
            if file_path != "#":
                sys.path.insert(0, file_path)
                base = DBASE.open('Anna')

                if base is not None:
                    return base
                else:
                    error(
                        'Cannot find Anna file in {}'
                        .format(file_path))
                    return None

            else:
                base = DBASE.open('Anna')
                if base is not None:
                    return base
                else:
                    error(
                        'Cannot find Anna file in {}'
                        .format(file_path))
                    return None

    # ______________________________________
    def SaveResult(self, result, result_path):
        """Add result to RootShelve file result.

        The method create / get a RootShelve file in the local directory
        called AnnaResults.

        Arguments:
            result {[type]} -- must inherit from TObject
            result_path {[type]} -- path inside AnnaResults.root
        """

        # Create / get results file in the local directory """
        db = self.GetResultFile()

        if db is not None:
            debug('result : {}'.format(result))

            # Check if file exists
            try:
                o = db[str(result_path + '/' + result.GetName())]
            except KeyError:
                print("No object in {}/{}".format(result_path, result.GetName()))
                o = None

            if o is not None:
                print("Replacing {}/{}".format(result_path, result.GetName()))
                del o

            db[str(result_path + '/' + result.GetName())] = result
            if db[str(result_path + '/' + result.GetName())] is not None:
                print("+++result {}/{} adopted".format(result_path, result.GetName()))

            else:
                error("Could not adopt result {}".format(result.GetName()))
                db.close()
                return

        else:
            error("Error creating result file")
            db.close()
            return

        db.close()

# =============================================================================
# The END
# =============================================================================
