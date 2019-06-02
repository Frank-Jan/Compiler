# from src.AST.Arg import Arg
from src.AST.Types import *
from src.AST.ASTNode import varGen
# import copy
import src.llvm2mips.MipsInstructions as MIPS
# import src.llvm2mips.Registry as R
# import src.llvm2mips.llvmToMips as llvm2mips

class LLVMInstr:

    def __init__(self):
        self.line = 0
        self.function = None

    def toMips(self, builder):
        print("Warning: toMips not yet implemented for llvm object: {}".format(type(self)))
        return None

    def setFunction(self, func):
        self.function = func


class Alloca(LLVMInstr):

    def __init__(self, result, _type):
        LLVMInstr.__init__(self)
        self.result = result
        self.type = _type
        self.align = _type.getAlign()

    def toMips(self, builder):
        r_result, code = builder.GetSavedRegister(str(self.result), self.line)
        code += MIPS.moveSP(builder.registry, 1)
        code += MIPS.M_move(r_result, 29)
        # code += mips.M_sw(r_result, R.SPtoIndex(), 0) # only allocate space
        return code

    def __str__(self):
        tmpType = self.type.toLLVM()
        if not isinstance(tmpType, ARRAY):
            return "%" + str(self.result) + " = alloca " + str(tmpType) + ", align " + str(self.align) + "\n"
        else:
            # %6 = alloca [5 x i32], align 16
            return "%" + str(self.result) + " = alloca " + str(tmpType) + ", align " + (self.type.size - 1) * str(
                self.align) + "\n"


class Store(LLVMInstr):

    def __init__(self, _type, _from, _to, lit=False):
        LLVMInstr.__init__(self)
        self.type = _type
        self._from = _from
        self._to = _to
        self.align = _type.getAlign()
        self.lit = lit

    def toMips(self, builder):
        mips = []
        r_to, code = builder.GetVariable(str(self._to), self.line)
        mips += code
        if self.lit:
            r_from = builder.GetTemporaryRegister()
            mips += MIPS.M_addi(0, self._from, r_from)
        else:
            r_from, code = builder.GetVariable(str(self._from), self.line)
            mips += code
        mips += MIPS.M_sw(r_from, r_to, 0)
        return mips

    def __str__(self):
        tmpType = self.type.toLLVM()
        if self.lit:
            return "store " + str(tmpType) + " " + str(self._from) + ", " + str(tmpType) + "* %" + str(
                self._to) + ", align " + str(self.align) + "\n"
        else:
            return "store " + str(tmpType) + " %" + str(self._from) + ", " + str(tmpType) + "* %" + str(
                self._to) + ", align " + str(self.align) + "\n"


class Load(LLVMInstr):

    def __init__(self, result, _type, var):
        LLVMInstr.__init__(self)
        self.result = result
        self.type = _type
        self.var = var
        self.align = _type.getAlign()

    # def toMips(self, builder):
    #

    def __str__(self):
        tmpType = self.type.toLLVM()
        return "%" + str(self.result) + " = load " + str(tmpType) + ", " + str(tmpType) + "* %" + str(
            self.var) + ", align " + str(self.align) + "\n"


class Declare(LLVMInstr):

    def __init__(self, _type, name, args):
        LLVMInstr.__init__(self)
        self.type = _type
        self.name = name
        self.args = args  # arg has _type, oldname and newname

    def __str__(self):
        tmpType = self.type.toLLVM()
        ll = "declare " + str(tmpType) + " @" + str(self.name) + "("
        for arg in self.args:
            ll += str(arg.toLLVM()) + ", "
        if len(self.args) != 0:
            ll = ll[:-2]
        ll += ")\n\n"
        return ll


class Define(LLVMInstr):

    def __init__(self, _type, name, args, stats):
        LLVMInstr.__init__(self)
        self.type = _type
        self.name = name
        self.args = args  # arg has _type, oldname and newname
        self.stats = stats

    def __iter__(self):
        return self.stats.__iter__()

    def __str__(self):
        tmpType = self.type.toLLVM()
        ll = "define " + str(tmpType) + " @" + str(self.name) + "("
        for arg in self.args:
            ll += str(arg.type.toLLVM()) + " %" + str(arg.tempName) + ", "
        if len(self.args) != 0:
            ll = ll[:-2]
        ll += ") {\n"

        # load values from newNames into oldNames
        load = []
        for arg in self.args:
            load.append(Alloca(arg.ogName, arg.type))
            load.append(Store(arg.type, arg.tempName, arg.ogName))
        self.stats = load + self.stats

        for stat in self.stats:
            stat.setFunction(self)  # set function
            if isinstance(stat, Str) or isinstance(stat, Array):
                ll = str(stat) + ll
            else:
                ll += str(stat)
        ll += "}\n\n"
        return ll


class endDefine(LLVMInstr):

    def __init__(self, define):
        LLVMInstr.__init__(self)
        self.beginDefine = define


class Call(LLVMInstr):  # %2 = call i32 @test()

    def __init__(self, result, _type, name, args):
        self.result = result
        self.type = _type
        self.name = name
        self.args = args  # arg has _type, oldname and newname

    def __str__(self):
        tmpType = self.type.toLLVM()
        ll = "%" + str(self.result) + " = call " + str(tmpType) + " @" + str(self.name) + "("
        for arg in self.args:
            if arg.lit:
                ll += str(arg.type.toLLVM()) + " " + str(arg.ogName) + ", "
            else:
                ll += str(arg.type.toLLVM()) + " %" + str(arg.ogName) + ", "
        if len(self.args) != 0:
            ll = ll[:-2]
        ll += ")\n"
        return ll


# ret i32 %6 | ret i32 0 | ret void
class Return(LLVMInstr):

    def __init__(self, _type, var, lit=False):
        LLVMInstr.__init__(self)
        self.type = _type
        self.var = var  # in case of void var = ""
        self.lit = lit

    def __str__(self):
        tmpType = self.type.toLLVM()
        retVal = ""
        if self.lit == True:
            retVal = str(self.var)
        else:
            retVal = "%" + str(self.var)

        return "ret " + str(tmpType) + " " + str(retVal) + "\n"


# ARITHMETIC
########################################################################
class Arithmetic(LLVMInstr):

    def __init__(self, result, op, _type, val1, val2, lit1=False, lit2=False):
        LLVMInstr.__init__(self)
        self.result = result
        self.op = op
        self.type = _type
        self.val1 = val1
        self.val2 = val2
        self.lit1 = lit1
        self.lit2 = lit2

    def __str__(self):
        tmpType = self.type.toLLVM()
        lit1 = "%"
        lit2 = "%"
        if self.lit1:
            lit1 = ""
        if self.lit2:
            lit2 = ""
        return "%" + str(self.result) + " = " + str(self.op) + " " + str(tmpType) + " " + lit1 + str(
            self.val1) + ", " + lit2 + str(self.val2) + "\n"


class Add(Arithmetic):

    def __init__(self, result, _type, val1, val2, lit1=False, lit2=False):
        Arithmetic.__init__(self, result, _type.getAdd(), _type, val1, val2, lit1, lit2)


class Sub(Arithmetic):

    def __init__(self, result, _type, val1, val2, lit1=False, lit2=False):
        Arithmetic.__init__(self, result, _type.getSub(), _type, val1, val2, lit1, lit2)


class Mul(Arithmetic):

    def __init__(self, result, _type, val1, val2, lit1=False, lit2=False):
        Arithmetic.__init__(self, result, _type.getMul(), _type, val1, val2, lit1, lit2)


class Div(Arithmetic):

    def __init__(self, result, _type, val1, val2, lit1=False, lit2=False):
        Arithmetic.__init__(self, result, _type.getDiv(), _type, val1, val2, lit1, lit2)


########################################################################

# br i1 %5, label %6, label %7 | br label %9
class Branch(LLVMInstr):

    def __init__(self, label1, label2=None, var=None):
        LLVMInstr.__init__(self)
        self.var = var
        self.label1 = label1
        self.label2 = label2

    def __str__(self):
        if self.var is None and self.label2 is None:
            return "br label %" + str(self.label1.label) + "\n"
        else:
            return "br i1 %" + str(self.var) + ", label %" + str(self.label1.label) + ", label %" + str(
                self.label2.label) + "\n"


# %4 = icmp slt i32 %3, 3
class Icmp(LLVMInstr):

    def __init__(self, op, _type, val1, val2, lit1=False, lit2=False):
        LLVMInstr.__init__(self)
        self.result = varGen.getNewVar(varGen)
        self.op = op
        self.type = _type
        self.val1 = val1
        self.val2 = val2
        self.lit1 = lit1
        self.lit2 = lit2
        self.label0 = varGen.getNewLabel(varGen)

    def __str__(self):
        # %5 = icmp eq i32 1, %4
        tmpType = self.type.toLLVM()
        lit1 = "%"
        lit2 = "%"
        if self.lit1:
            lit1 = ""
        if self.lit2:
            lit2 = ""
        ll = "%" + str(self.result) + " = icmp " + str(self.op) + " " + str(tmpType) + " " + lit1 + str(
            self.val1) + ", " + lit2 + str(self.val2) + "\n"
        return ll


# LabelName:
class Label(LLVMInstr):

    def __init__(self):
        LLVMInstr.__init__(self)
        self.label = varGen.getNewLabel(varGen)

    def __str__(self):
        return "\n" + self.label + ":\n"


# For printf and scanf
##############################################################################################
class Str(LLVMInstr):

    def __init__(self, name, string, count):
        LLVMInstr.__init__(self)
        self.name = name
        self.string = string
        self.count = count  # om wille van \00 einde -2 voor "c"" en -2 voor "\00

    def __str__(self):
        # @.str = private unnamed_addr constant [25 x i8] c"Hey a uis gelijk aan: %d\00", align 1
        tmpString = "c\"" + self.string + "\\00"
        self.returnType = "[" + str(self.count) + " x i8]"
        return "@." + self.name + " = private unnamed_addr constant " + self.returnType + " " + tmpString + "\", align 1\n\n"


class CallF(LLVMInstr):

    def __init__(self, result, args, Str, printf=True):
        LLVMInstr.__init__(self)
        self.result = result
        self.args = args
        self.string = Str.name
        self.count = Str.count
        self.printf = printf

    def __str__(self):
        # %var-8 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([25 x i8], [25 x i8]* @.str, i32 0, i32 0), i32 %var-7)
        op = "scanf"
        if self.printf:
            op = "printf"
        ll = "%" + self.result + " = call i32 (i8*, ...) @" + op + "(i8* getelementptr inbounds ([" + str(
            self.count) + " x i8], [" + str(
            self.count) + " x i8]* @." + self.string + ", i32 0, i32 0)"

        for arg in self.args:
            ll += ", " + arg[0] + " %" + arg[1]

        return ll + ")\n"


class Sext(LLVMInstr):

    def __init__(self, result, _type, var):
        LLVMInstr.__init__(self)
        self.result = result
        self.type = _type
        self.var = var

    def __str__(self):
        # %4 = sext i8 %3 to i32
        tmpType = self.type.toLLVM()
        return "%" + self.result + " = sext " + tmpType + " %" + str(self.var) + " to i32\n"


class Fpext(LLVMInstr):

    def __init__(self, result, _type, var):
        LLVMInstr.__init__(self)
        self.result = result
        self.type = _type
        self.var = var

    def __str__(self):
        # %7 = fpext float %6 to double
        tmpType = self.type.toLLVM()
        return "%" + self.result + " = fpext " + tmpType + " %" + str(self.var) + " to double\n"


# ARRAYS
#####################################################################################################
class Array(LLVMInstr):

    def __init__(self, name, length, _type, elements):
        LLVMInstr.__init__(self)
        self.name = name
        self.length = length
        self.type = _type
        self.type.size = self.length
        self.elements = elements
        for i in range(len(elements), self.length):
            self.elements.append(0)

    def __str__(self):
        # @main.arr1 = private unnamed_addr constant [5 x i32] [i32 1, i32 2, i32 3, i32 4, i32 5], align 16
        tmpType = self.type.getBase().toLLVM()
        ll = "@." + self.name + " = private unnamed_addr constant [" + str(self.length) + " x " + tmpType + "] ["

        for el in self.elements:
            ll += tmpType + " " + str(el) + ", "
        ll = ll[:-2]
        ll += "], align " + str(self.type.getAlign()) + "\n\n"
        return ll


class Bitcast(LLVMInstr):

    def __init__(self, result, _type, var):
        LLVMInstr.__init__(self)
        self.result = result
        self.type = _type
        self.var = var

    def __str__(self):
        #  %4 = bitcast [2 x i32]* %3 to i8*
        tmpType = self.type.toLLVM()
        return "%" + self.result + " = bitcast " + tmpType + "* %" + self.var + " to i8*\n"


class CallA(LLVMInstr):

    def __init__(self, var, type, arrayName):
        LLVMInstr.__init__(self)
        self.var = var
        self.type = type
        self.arrayName = arrayName

    def __str__(self):
        #  call void @llvm.memcpy.p0i8.p0i8.i64(i8* %5, i8* bitcast ([2 x i32]* @main.arr2 to i8*), i64 8, i32 4, i1 false)
        tmpType = self.type.toLLVM()
        ll = "call void @llvm.memcpy.p0i8.p0i8.i64(i8* %" + str(
            self.var) + ", i8* bitcast (" + str(tmpType) + "* @." + self.arrayName + " to i8*), i64 8, i32 4, i1 false)"
        return ll + "\n"


class Memcpy(LLVMInstr):

    def __str__(self):
        return "declare void @llvm.memcpy.p0i8.p0i8.i64(i8* nocapture writeonly, i8* nocapture readonly, i64, i32, i1)\n\n"


class Getel(LLVMInstr):

    def __init__(self, result, type, var, position):
        LLVMInstr.__init__(self)
        self.result = result
        self.type = type
        self.var = var
        self.position = position

    def __str__(self):
        # %8 = getelementptr inbounds [3 x i32], [3 x i32]* %2, i64 0, i64 1
        tmpType = self.type.toLLVM()
        return "%" + str(self.result) + " = getelementptr inbounds " + str(tmpType) + ", " + str(tmpType) + "* %" + str(
            self.var) + ", i64 0, i64 " + str(self.position) + "\n"
